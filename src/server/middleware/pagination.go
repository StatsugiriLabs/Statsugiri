package middleware

import (
	"net/http"
    "go.mongodb.org/mongo-driver/mongo/options"	
	"strconv"
)

// https://stackoverflow.com/a/64602288
func Pagination(r *http.Request, FindOptions *options.FindOptions) (int64, int64) {
    if r.URL.Query().Get("page") != "" && r.URL.Query().Get("limit") != "" {
        page, _ := strconv.ParseInt(r.URL.Query().Get("page"), 10, 32)
        limit, _ := strconv.ParseInt(r.URL.Query().Get("limit"), 10, 32)
        if page == 1 {
            FindOptions.SetSkip(0)
            FindOptions.SetLimit(limit)
            return page, limit
        }

        FindOptions.SetSkip((page - 1) * limit)
        FindOptions.SetLimit(limit)
        return page, limit

    }
    FindOptions.SetSkip(0)
    FindOptions.SetLimit(0)
    return 0, 0
}