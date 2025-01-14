import re

from datadog_checks.checks import AgentCheck

# Paths
COUCHBASE_STATS_PATH = '/pools/default'
COUCHBASE_VITALS_PATH = '/admin/vitals'

# Service Checks
SERVICE_CHECK_NAME = 'couchbase.can_connect'
NODE_CLUSTER_SERVICE_CHECK_NAME = 'couchbase.by_node.cluster_membership'
NODE_HEALTH_SERVICE_CHECK_NAME = 'couchbase.by_node.health'

NODE_MEMBERSHIP_TRANSLATION = {
    'active': AgentCheck.OK,
    'inactiveAdded': AgentCheck.WARNING,
    'activeFailed': AgentCheck.CRITICAL,
    None: AgentCheck.UNKNOWN,
}

NODE_HEALTH_TRANSLATION = {
    'healthy': AgentCheck.OK,
    'warmup': AgentCheck.OK,
    'unhealthy': AgentCheck.CRITICAL,
    None: AgentCheck.UNKNOWN,
}

# Events
SOURCE_TYPE_NAME = 'couchbase'

# Selected metrics to send amongst all the bucket stats, after name normalization
BUCKET_STATS = {
    "avg_bg_wait_time",
    "avg_disk_commit_time",
    "avg_disk_update_time",
    "bg_wait_total",
    "bytes_read",
    "bytes_written",
    "cas_badval",
    "cas_hits",
    "cas_misses",
    "cmd_get",
    "cmd_set",
    "couch_docs_actual_disk_size",
    "couch_docs_data_size",
    "couch_docs_disk_size",
    "couch_docs_fragmentation",
    "couch_spatial_data_size",
    "couch_spatial_disk_size",
    "couch_spatial_ops",
    "couch_total_disk_size",
    "couch_views_data_size",
    "couch_views_disk_size",
    "couch_views_fragmentation",
    "couch_views_ops",
    "cpu_idle_ms",
    "cpu_utilization_rate",
    "curr_connections",
    "curr_items_tot",
    "curr_items",
    "decr_hits",
    "decr_misses",
    "delete_hits",
    "delete_misses",
    "disk_commit_count",
    "disk_update_count",
    "disk_write_queue",
    "ep_bg_fetched",
    "ep_cache_miss_rate",
    "ep_cache_miss_ratio",
    "ep_dcp_fts_backoff",
    "ep_dcp_fts_count",
    "ep_dcp_fts_items_remaining",
    "ep_dcp_fts_items_sent",
    "ep_dcp_fts_producer_count",
    "ep_dcp_fts_total_bytes",
    "ep_dcp_2i_backoff",
    "ep_dcp_2i_count",
    "ep_dcp_2i_items_remaining",
    "ep_dcp_2i_items_sent",
    "ep_dcp_2i_producer_count",
    "ep_dcp_2i_total_bytes",
    "ep_dcp_other_backoff",
    "ep_dcp_other_count",
    "ep_dcp_other_items_remaining",
    "ep_dcp_other_items_sent",
    "ep_dcp_other_producer_count",
    "ep_dcp_other_total_bytes",
    "ep_dcp_replica_backoff",
    "ep_dcp_replica_count",
    "ep_dcp_replica_items_remaining",
    "ep_dcp_replica_items_sent",
    "ep_dcp_replica_producer_count",
    "ep_dcp_replica_total_bytes",
    "ep_dcp_views_backoff",
    "ep_dcp_views_count",
    "ep_dcp_views_items_remaining",
    "ep_dcp_views_items_sent",
    "ep_dcp_views_producer_count",
    "ep_dcp_views_total_bytes",
    "ep_dcp_xdcr_backoff",
    "ep_dcp_xdcr_count",
    "ep_dcp_xdcr_items_remaining",
    "ep_dcp_xdcr_items_sent",
    "ep_dcp_xdcr_producer_count",
    "ep_dcp_xdcr_total_bytes",
    "ep_diskqueue_drain",
    "ep_diskqueue_fill",
    "ep_diskqueue_items",
    "ep_flusher_todo",
    "ep_item_commit_failed",
    "ep_kv_size",
    "ep_max_size",
    "ep_mem_high_wat",
    "ep_mem_low_wat",
    "ep_meta_data_memory",
    "ep_num_non_resident",
    "ep_num_ops_del_meta",
    "ep_num_ops_del_ret_meta",
    "ep_num_ops_get_meta",
    "ep_num_ops_set_meta",
    "ep_num_ops_set_ret_meta",
    "ep_num_value_ejects",
    "ep_oom_errors",
    "ep_ops_create",
    "ep_ops_update",
    "ep_overhead",
    "ep_queue_size",
    "ep_resident_items_rate",
    "ep_tap_replica_queue_drain",
    "ep_tap_total_queue_drain",
    "ep_tap_total_queue_fill",
    "ep_tap_total_total_backlog_size",
    "ep_tmp_oom_errors",
    "ep_vb_total",
    "evictions",
    "get_hits",
    "get_misses",
    "hibernated_requests",
    "hibernated_waked",
    "hit_ratio",
    "incr_hits",
    "incr_misses",
    "mem_actual_free",
    "mem_actual_used",
    "mem_free",
    "mem_total",
    "mem_used",
    "mem_used_sys",
    "misses",
    "ops",
    "page_faults",
    "replication_docs_rep_queue",
    "replication_meta_latency_aggr",
    "rest_requests",
    "swap_total",
    "swap_used",
    "vb_active_eject",
    "vb_active_itm_memory",
    "vb_active_meta_data_memory",
    "vb_active_num_non_resident",
    "vb_active_num",
    "vb_active_ops_create",
    "vb_active_ops_update",
    "vb_active_queue_age",
    "vb_active_queue_drain",
    "vb_active_queue_fill",
    "vb_active_queue_size",
    "vb_active_resident_items_ratio",
    "vb_avg_active_queue_age",
    "vb_avg_pending_queue_age",
    "vb_avg_replica_queue_age",
    "vb_avg_total_queue_age",
    "vb_pending_curr_items",
    "vb_pending_eject",
    "vb_pending_itm_memory",
    "vb_pending_meta_data_memory",
    "vb_pending_num_non_resident",
    "vb_pending_num",
    "vb_pending_ops_create",
    "vb_pending_ops_update",
    "vb_pending_queue_age",
    "vb_pending_queue_drain",
    "vb_pending_queue_fill",
    "vb_pending_queue_size",
    "vb_pending_resident_items_ratio",
    "vb_replica_curr_items",
    "vb_replica_eject",
    "vb_replica_itm_memory",
    "vb_replica_meta_data_memory",
    "vb_replica_num_non_resident",
    "vb_replica_num",
    "vb_replica_ops_create",
    "vb_replica_ops_update",
    "vb_replica_queue_age",
    "vb_replica_queue_drain",
    "vb_replica_queue_fill",
    "vb_replica_queue_size",
    "vb_replica_resident_items_ratio",
    "vb_total_queue_age",
    "xdc_ops",
}
# Selected metrics of the query monitoring API
# See https://developer.couchbase.com/documentation/server/4.5/tools/query-monitoring.html
QUERY_STATS = {
    'cores',
    'cpu_sys_percent',
    'cpu_user_percent',
    'gc_num',
    'gc_pause_percent',
    'gc_pause_time',
    'memory_system',
    'memory_total',
    'memory_usage',
    'request_active_count',
    'request_completed_count',
    'request_per_sec_15min',
    'request_per_sec_1min',
    'request_per_sec_5min',
    'request_prepared_percent',
    'request_time_80percentile',
    'request_time_95percentile',
    'request_time_99percentile',
    'request_time_mean',
    'request_time_median',
    'total_threads',
}

TO_SECONDS = {'ns': 1e9, 'us': 1e6, 'ms': 1e3, 's': 1}

SECONDS_VALUE_PATTERN = re.compile(r'(\d+(\.\d+)?)(\D+)')
