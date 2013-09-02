import jupi
j = jupi.Jupi("localhost", 8080, 8081)
j.add_binding(None, 1, lambda : j.is_bad("Job1") or j.is_bad("Job2"))
j.add_binding(None, 2, lambda : j.is_good("Job1"))
j.start()
