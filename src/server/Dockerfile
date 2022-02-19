FROM golang:1.17-alpine

# Enable go modules
ENV GO111MODULE=on

# Copy source code
WORKDIR /
COPY . .

# Expose port
EXPOSE 3000

# Build and run server binary
RUN go build -o main main.go
