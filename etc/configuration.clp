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
    (name "zabbix")
    (desc "Zabbix protocol driver")
)
(driver
    (type "protocol")
    (name "zabbix_json")
    (desc "Zabbix JSON packer")
)
;;
;; Define drivers chain
;;
(driver_chain
    (name "zabbix_active_proxy")
    (chain "zabbix_json", "zabbix")
)
;;
;; Start the daemons
;;
(daemon
    (main "dummy.daemon")
    (name "dummy_daemon")
    (desc "Dummy ZAP daemon")
    (args "a" "b" "c")
)
(daemon
    (main "zabbix.heartbeat")
    (name "Heartbeat")
    (desc "Zabbix Heartbeat daemon")
    (args "dev-zap")
)
;;
;; Execute this code during ZAP startup
;;

(start
    (name "dummy.main")
    (desc "Dummy startup code")
    (args "b" 1 2 3.14 TRUE)
)

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
)