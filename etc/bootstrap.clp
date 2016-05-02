;;
;; Bootstrapping US
;;


;;
;; Defining Template for the facts about application
;;
(deftemplate application
    ;  Application name
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    ; Application description
    (slot desc
        (type STRING)
        (default ?DERIVE)
    )
    ; Application POC
    (slot poc
        (type STRING)
        (default "Administrator")
    )
    ; POC e-mail
    (slot email
        (type STRING)
        (default ?DERIVE)
    )
    ; POC phone
    (slot phone
        (type STRING)
        (default ?DERIVE)
    )
)
;;
;; PYTHON modules loaded into USS
;;
(deftemplate py_module
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot path
        (type STRING)
        (default ?DERIVE)

    )
)

;;
;; PYTHON driver path for the drivers loaded into USS
;;
(deftemplate driver_path
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot path
        (type STRING)
        (default ?DERIVE)

    )
)
;;
;; PYTHON drivers loaded into USS
;;
(deftemplate driver
    (slot type
        (type STRING)
        (default ?DERIVE)
    )
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot desc
        (type STRING)
        (default "")
    )
)


;;
;; USS Configuration facts
;;
(deftemplate cfg
    (slot section
        (type STRING)
        (default "main")
    )
    (slot key
        (type STRING)
        (default ?DERIVE)
    )
    (slot note
        (type STRING)
        (default "")
    )
)
;;
;; USS startup modules
;;
(deftemplate start
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot desc
        (type STRING)
        (default "")

    )
)

;;
;; Load the specific CLIPS integration module
;;

(deftemplate clips_mod
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot desc
        (type STRING)
        (default "")

    )
)

;;
;; Network BIND's
;;
(deftemplate listen
    (slot name
        (type STRING)
        (default ?DERIVE)
    )
    (slot interface
        (type STRING)
        (default ?DERIVE)
    )
    (slot port
        (type INTEGER)
    )
)