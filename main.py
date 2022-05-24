from __init__ import createApp
import os


if __name__ == "__main__":
    app = createApp()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port,debug=False)