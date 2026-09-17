/**
 * Smart NER Logistics Control Platform
 * Feature A: Offline-First Local Cache & Reconnection Telemetry Sync Manager
 *
 * Supported Features:
 * - Stores unified trip plan locally under `smart_ner_cached_plan`:
 *   (selected_route, alt_routes, risk_score, distance, cargo_allocation, packed_items, waiting_items, utilization).
 * - Discrete sync states: "Pending", "Syncing", "Synced", "Failed / retrying".
 * - Standalone offline driver execution for route inspection, checkpoint logging, and delivery confirmation.
 * - Automatic background queue flush and sync upon reconnection.
 */

const STORAGE_KEYS = {
  CACHED_TRIP: "smart_ner_cached_trip",
  CACHED_PLAN: "smart_ner_cached_plan",
  SYNC_QUEUE: "smart_ner_offline_sync_queue",
  CONNECTIVITY_MODE: "smart_ner_connectivity_mode",
  SYNC_STATUS: "smart_ner_sync_status"
};

class OfflineSyncManager {
  constructor() {
    this.isOnline = localStorage.getItem(STORAGE_KEYS.CONNECTIVITY_MODE) !== "Offline";
    this.syncQueue = this.loadSyncQueue();
    this.syncStatus = this.syncQueue.length > 0 ? "Pending" : "Synced";

    // Setup browser online/offline event listeners
    if (typeof window !== "undefined") {
      window.addEventListener("online", () => this.handleNetworkChange(true));
      window.addEventListener("offline", () => this.handleNetworkChange(false));
    }
  }

  // Load queued actions from localStorage
  loadSyncQueue() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.SYNC_QUEUE);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.warn("Failed to load sync queue:", e);
      return [];
    }
  }

  // Save current sync queue
  saveSyncQueue() {
    try {
      localStorage.setItem(STORAGE_KEYS.SYNC_QUEUE, JSON.stringify(this.syncQueue));
      if (this.syncQueue.length > 0 && this.syncStatus === "Synced") {
        this.setSyncStatus("Pending");
      }
    } catch (e) {
      console.error("Failed to save sync queue:", e);
    }
  }

  // Update sync status and notify UI components
  setSyncStatus(status) {
    this.syncStatus = status;
    try {
      localStorage.setItem(STORAGE_KEYS.SYNC_STATUS, status);
    } catch (e) {}

    if (typeof window !== "undefined") {
      const evt = new CustomEvent("smart_ner_sync_status_changed", {
        detail: { status: this.syncStatus, queueLength: this.syncQueue.length, isOnline: this.isOnline }
      });
      window.dispatchEvent(evt);
    }
  }

  getSyncStatus() {
    return this.syncStatus;
  }

  // Cache the combined trip plan (Feature A Offline Requirement)
  cacheCombinedPlan(planData) {
    try {
      const routeInfo = planData.route || {};
      const allocInfo = planData.allocation || {};

      const standardizedPlan = {
        id: allocInfo.manifest_id || `PLAN-${Date.now()}`,
        selected_route: routeInfo.selected_route || {},
        alt_routes: routeInfo.alt_routes || [],
        risk_score: routeInfo.risk_score || (routeInfo.selected_route ? routeInfo.selected_route.risk_score : 0.0),
        distance_km: routeInfo.distance_km || (routeInfo.selected_route ? routeInfo.selected_route.total_distance_km : 0.0),
        predicted_risk: routeInfo.predicted_risk || (routeInfo.selected_route ? routeInfo.selected_route.predicted_risk : {}),
        cargo_allocation: allocInfo,
        packed_items: allocInfo.packed_items || allocInfo.allocated_items || [],
        waiting_items: allocInfo.waiting_items || [],
        utilization: allocInfo.utilization || {
          payload_utilization_pct: allocInfo.payload_utilization_pct || 0,
          volume_utilization_pct: allocInfo.volume_utilization_pct || 0,
          allocated_payload_kg: allocInfo.allocated_payload_kg || 0,
          max_payload_kg: allocInfo.max_payload_kg || 0,
          allocated_volume_m3: allocInfo.allocated_volume_m3 || 0,
          max_volume_m3: allocInfo.max_volume_m3 || 0
        },
        cached_at: new Date().toISOString()
      };

      localStorage.setItem(STORAGE_KEYS.CACHED_PLAN, JSON.stringify(standardizedPlan));
      console.log("Cached combined plan stored under smart_ner_cached_plan:", standardizedPlan.id);
      return standardizedPlan;
    } catch (e) {
      console.error("Failed to cache combined plan:", e);
      return null;
    }
  }

  // Retrieve cached combined plan
  getCachedPlan() {
    try {
      const raw = localStorage.getItem(STORAGE_KEYS.CACHED_PLAN);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      console.warn("Failed to retrieve cached plan:", e);
      return null;
    }
  }

  // Cache an assigned trip locally for driver HUD
  cacheTrip(tripData) {
    try {
      localStorage.setItem(STORAGE_KEYS.CACHED_TRIP, JSON.stringify(tripData));
      console.log("Trip successfully cached for offline use:", tripData.id);
    } catch (e) {
      console.error("Failed to cache trip:", e);
    }
  }

  // Get cached trip data
  getCachedTrip() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CACHED_TRIP);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  }

  // Set connectivity mode (simulates mountain valley cellular drop / restoration)
  setConnectivity(mode) {
    const wasOffline = !this.isOnline;
    this.isOnline = mode === "Online";
    localStorage.setItem(STORAGE_KEYS.CONNECTIVITY_MODE, mode);

    if (this.isOnline && wasOffline) {
      // Reconnected! Automatically sync queued updates
      this.flushSyncQueue();
    } else if (!this.isOnline && this.syncQueue.length > 0) {
      this.setSyncStatus("Pending");
    }

    if (typeof window !== "undefined") {
      window.dispatchEvent(new CustomEvent("smart_ner_connectivity_changed", {
        detail: { isOnline: this.isOnline, mode: mode }
      }));
    }
  }

  handleNetworkChange(online) {
    this.setConnectivity(online ? "Online" : "Offline");
  }

  // Queue a driver action (checkpoint pass or cargo delivery) when offline
  recordDriverAction(action) {
    const record = {
      id: "ACT-" + Date.now(),
      type: action.type, // "CHECKPOINT" or "DELIVERY"
      payload: action.payload,
      timestamp: new Date().toISOString(),
      offlineRecorded: !this.isOnline
    };

    this.syncQueue.push(record);
    this.saveSyncQueue();
    this.setSyncStatus(this.isOnline ? "Syncing" : "Pending");

    // Also update locally cached trip so the driver sees immediate UI feedback offline
    const trip = this.getCachedTrip();
    if (trip) {
      if (action.type === "CHECKPOINT") {
        const cp = trip.checkpoints.find(c => c.name === action.payload.checkpointName);
        if (cp) {
          cp.status = "Passed";
          cp.passed_at = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
      } else if (action.type === "DELIVERY") {
        const items = trip.manifest?.allocated_items || trip.manifest?.packed_items || [];
        const item = items.find(i => i.id === action.payload.cargoId);
        if (item) {
          item.status = "Delivered";
        }
      }
      this.cacheTrip(trip);
    }

    // Also update cached combined plan if present
    const plan = this.getCachedPlan();
    if (plan && plan.packed_items) {
      if (action.type === "DELIVERY") {
        const pItem = plan.packed_items.find(i => i.id === action.payload.cargoId);
        if (pItem) {
          pItem.status = "Delivered";
          this.cacheCombinedPlan({ route: { selected_route: plan.selected_route }, allocation: plan });
        }
      }
    }

    // If online, immediately try syncing
    if (this.isOnline) {
      this.flushSyncQueue();
    }

    return record;
  }

  // Flush queued telemetry to the backend API upon reconnection
  async flushSyncQueue(apiBaseUrl = "") {
    if (this.syncQueue.length === 0) {
      this.setSyncStatus("Synced");
      return { syncedCount: 0, message: "Sync queue is empty.", success: true };
    }

    if (!this.isOnline) {
      this.setSyncStatus("Pending");
      return { syncedCount: 0, message: "Device is offline. Updates are queued.", success: false };
    }

    this.setSyncStatus("Syncing");

    const trip = this.getCachedTrip();
    const tripId = trip ? trip.id : "TRIP-1024";

    const completedCheckpoints = this.syncQueue
      .filter(a => a.type === "CHECKPOINT")
      .map(a => a.payload.checkpointName);

    const deliveredCargo = this.syncQueue
      .filter(a => a.type === "DELIVERY")
      .map(a => a.payload.cargoId);

    const payload = {
      trip_id: tripId,
      driver_id: trip ? trip.driver_id : "DRV-NER-101",
      current_lat: 27.0844,
      current_lng: 93.6053,
      timestamp: new Date().toISOString(),
      completed_checkpoint_names: completedCheckpoints,
      delivered_cargo_item_ids: deliveredCargo,
      local_offline_notes: `Batch synced ${this.syncQueue.length} offline driver telemetry events after reconnecting.`,
      battery_level_pct: 82
    };

    try {
      const resp = await fetch(`${apiBaseUrl}/api/driver/sync-telemetry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (resp.ok) {
        const data = await resp.json();
        const count = this.syncQueue.length;
        this.syncQueue = [];
        this.saveSyncQueue();
        this.setSyncStatus("Synced");
        return { syncedCount: count, result: data, success: true };
      } else {
        throw new Error(`Sync failed with HTTP ${resp.status}`);
      }
    } catch (err) {
      console.warn("Could not sync online, preserving local queue:", err);
      this.setSyncStatus("Failed / retrying");
      return { syncedCount: 0, success: false, error: err.message };
    }
  }
}

// Global instance
window.offlineSyncManager = new OfflineSyncManager();
