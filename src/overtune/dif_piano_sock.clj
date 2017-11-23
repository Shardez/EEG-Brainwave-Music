; Import libraries and packages
(import '(java.net ServerSocket Socket SocketException))
(import '(java.io DataInputStream BufferedInputStream))
(require '[clojure.string :as str])

; Start overtone and connect to separately started SuperCollider server at port 6888
(use 'overtone.core)
(connect-external-server 6888)

; load sampled-piano instument
(use 'overtone.inst.sampled-piano)

; Connect to Python app
(def IPaddress "localhost")
(def port 8885)
(def socket (Socket. IPaddress port))
(println "Connected:" (.isConnected socket))
(def inp (DataInputStream. (BufferedInputStream. (.getInputStream socket))))

; Declare initial values (for difference calculation)
(def oax 0.2)
(def obx 0.2)
(def ogx 0.2)
(def odx 0.2)
(def otx 0.2)
(def omx 50)
(println "Receiving brainwave transmission")

; Parse incoming string from Python app, use EEG data to calculate normalized difference between current (ax) and previous (oax) value, use it to schedule notes (as a product with current meditation value * 15), assign pitch and sustain parameters

;(recording-start "C:/Projects/Portfolio/EEG-Brainwave-Music/bw_musicsample.wav")
(while true
 (def response (.readLine inp))
 (def rline (str/split response #" "))
 (println "Output: " response)
 (def ax (Double/parseDouble (rline 0)))
 (def bx (Double/parseDouble (rline 1)))
 (def dx (Double/parseDouble (rline 2)))
 (def gx (Double/parseDouble (rline 3)))
 (def tx (Double/parseDouble (rline 4)))
 (def mx (Double/parseDouble (rline 5)))
 (def nx (Double/parseDouble (rline 6)))


 (def dax (/ (Math/abs (- oax ax)) oax))
 (def dbx (/ (Math/abs (- obx bx)) obx))
 (def dgx (/ (Math/abs (- ogx gx)) ogx))
 (def ddx (/ (Math/abs (- odx dx)) odx))
 (def dtx (/ (Math/abs (- otx tx)) otx))

 ;(def dmx (/ (Math/abs (- omx mx)) omx))
 ;(def dmx (* 1000 dmx))

 (def dmx (* 15 omx))

(let [time (now)]
 (at (+ (* ddx dmx) time)
  (sampled-piano :note (+ 21 (* 15 ddx)) :sustain (* 2 (float ddx)) :level (float ddx))
 )
 (at (+ (* dtx dmx) time)
  (sampled-piano :note (+ 35 (* 15 dtx)) :sustain (* 2 (float dtx)) :level (float dtx))
 )
 (at (+ (* dax dmx) time)
  (sampled-piano :note (+ 50 (* 15 dax)) :sustain (* 2 (float dax)) :level (float dax))
 )
 (at (+ (* dbx dmx) time)
  (sampled-piano :note (+ 65 (* 15 dbx)) :sustain (* 2 (float dbx)) :level (float dbx))
 )
(at (+ (* dgx dmx) time)
  (sampled-piano :note (+ 80 (* 15 dgx)) :sustain (* 2 (float dgx)) :level (float dgx))
 )

 (def oax (+ 0.000001 ax))
 (def obx (+ 0.000001 bx))
 (def ogx (+ 0.000001 gx))
 (def odx (+ 0.000001 dx))
 (def otx (+ 0.000001 tx))
 (def omx (+ 1 mx))
 )

)
;(recording-stop)
