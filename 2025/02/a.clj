; https://clojure.org/guides/learn/syntax
; https://learnxinyminutes.com/clojure
; https://clojure-doc.org/articles/cookbooks/files_and_directories/
; https://ericnormand.me/mini-guide/clojure-regex
;
; run with clojure -M a.clj

(defn to-range [l]
  (range
    (parse-long (l 1))
    (+ 1 (parse-long (l 2)))))

(def ids
  (apply concat
    (map to-range
      (re-seq
        #"(\d+)-(\d+)"
        (slurp "input")))))

(defn matches [pattern]
  (fn [id]
    (not (nil?
      (re-matches pattern (str id))))))

(def invalid-p1? (matches #"(\d+)\1" ))
(def invalid-p2? (matches #"(\d+)\1+"))

(println
  (apply + (filter invalid-p1? ids)))

(println
  (apply + (filter invalid-p2? ids)))
