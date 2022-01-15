package api

import (
	"fmt"
	"net/http"
)

func healthCheckFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "status ok")
}
