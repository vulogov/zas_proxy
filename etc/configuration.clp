;;
;; Application setup
;;
(application
    (name "test application")
    (desc "test application description")
    (poc "Vladimir Ulogov")
    (email "vladimir.ulogov@zabbix.com")
    (phone "+1-973-555-1122")
)

;;
;; Path for the Drivers
;;
(pythonpath
    (desc "Path to a ZAP modules")
    (path "/root/Src/zap_proxy/etc/python")
)

;;
;; Location of the loadable Python modules
;;

(py_module
    (name "Main PY modules")
    (path "/root/Src/zap_proxy/etc/zap_modules")
)

;;
;; Locations of the PYTHON-CLIPS integration
;;
(py_module
    (name "Main PYCLP bindings")
    (path "/root/Src/zap_proxy/etc/zap_clips")
)

;;
;; Load PYCLIPS binding
;;
(clips_mod
    (name "match")
    (desc "Pattern matching functions")
)

;;
;; Path for the Drivers
;;
(driver_path
    (name "Path for the main ZAP drivers")
    (path "/root/Src/zap_proxy/etc/zap_drivers")
)

;;
;; Load specific driver
;;
;(driver
;    (type "startup")
;    (name "dummy")
;    (desc "Dummy startup driver")
;    (args 1 2 3)
;)
(driver
    (type "protocol")
    (name "zabbix_trapper")
    (desc "Zabbix trapper protocol driver")
)
(driver
    (type "protocol")
    (name "zabbix_active_proxy")
    (desc "Zabbix Active Proxy protocol driver")
)
(driver
    (type "protocol")
    (name "zabbix_active_proxy_cfg")
    (desc "Zabbix Active Proxy Configuration protocol driver")
)
(driver
    (type "protocol")
    (name "zabbix")
    (desc "Zabbix protocol driver")
)
(driver
    (type "protocol")
    (name "zabbix_json")
    (desc "Zabbix JSON packer")
)
(driver
    (type "protocol")
    (name "zabbix_json_request")
    (desc "Zabbix JSON request handler")
)
(driver
    (type "protocol")
    (name "zabbix_json_timestamp")
    (desc "Zabbix JSON clock")
)
(driver
    (type "protocol")
    (name "zabbix_ns_stamp")
    (desc "Zabbix NS stamp")
)
(driver
    (type "protocol")
    (name "zabbix_json_host")
    (desc "Zabbix JSON Hostname")
)
(driver
    (type "protocol")
    (name "zabbix_json_host")
    (desc "Zabbix JSON Hostname")
)
(driver
    (type "protocol")
    (name "zabbix_status_update")
    (desc "Zabbix Update Host status")
)
(driver
    (type "db")
    (name "database_redis")
    (desc "Storing data into REDIS storage")
)
;;
;; Define drivers chain
;;
(driver_chain
    (name "zabbix_active_proxy")
    (chain "zabbix_json_request" "zabbix_json_host" "zabbix_status_update" "zabbix_json_timestamp" "zabbix_json" "zabbix")
)
(driver_chain
    (name "zabbix_json_timestamp")
    (chain "zabbix_ns_stamp")
)
(driver_chain
    (name "zabbix_active_proxy_cfg")
    (chain "zabbix_json_request" "zabbix_json_host" "zabbix_json_timestamp" "zabbix_json" "zabbix")
)
;;
;; Define DB linkage
;;
(db_link
    (name "database_redis")
    (desc "Everything is stored in REDIS")
    (src "*")
    (args "127.0.0.1" 6379)
)
;;
;; Start the daemons
;;
;(daemon
;    (main "dummy.daemon")
;    (name "dummy_daemon")
;    (desc "Dummy ZAP daemon")
;    (args "a" "b" "c")
;)
(daemon
    (main "zabbix.heartbeat")
    (name "Heartbeat")
    (desc "Zabbix Heartbeat daemon")
)
(daemon
    (main "zabbix.active_proxy")
    (name "ActiveProxy")
    (desc "Zabbix ActiveProxy daemon")
)
;;
;; Execute this code during ZAP startup
;;

;(start
;    (name "dummy.main")
;    (desc "Dummy startup code")
;    (args "b" 1 2 3.14 TRUE)
;)

;;
;; Now, configure the LISTEN interfaces
;;
(listen
    (name "trapper %d")
    (desc "Zabbix trapper interface")
    (interface "0.0.0.0")
    (port 11051)
)

;;
;; Zabbix servers
;;
(zabbix_server
    (name "dev.zabbix.us")
    (desc "Local Zabbix Server")
    (hostname "ZAP Active Proxy")
)

;;
;; Configuration facts
;;
(cfg
    (section "client")
    (key     "bufsize")
    (value    4096)
)
(cfg
    (section "heartbeat")
    (key     "beat")
    (value    60.0)
)
(cfg
    (section "client")
    (key     "timeout")
    (value    5.0)
)
(cfg
    (section "db")
    (key     "default_driver")
    (value    "database_redis")
)
(cfg
    (section "db")
    (key     "default_driver_args")
    (args    "127.0.0.1" 6379)
)
(cfg
    (section "active_proxy")
    (key     "cfg_update")
    (value    3.0)
)