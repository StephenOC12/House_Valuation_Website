from Website import StartApp

app = StartApp()

if __name__ == '__main__':
    #will only run if you run it directly from this file, not if you use main elsewhere
    app.run(debug=True)
    #Will update changes while the web server is still running
