import sys
import fire
from bharatwatch.core.database import init_db
from bharatwatch.core.orchestrator import run_all, run_module
from bharatwatch.core.healer import heal_monitor
from bharatwatch.api.main import app

class CLI:
    def init_db(self):
        init_db()
        print("Database initialized.")

    def run_all(self):
        init_db()
        run_all()

    def run_module(self, module: str):
        init_db()
        run_module(module)

    def heal_monitor(self):
        init_db()
        heal_monitor()

    def serve(self, host="127.0.0.1", port=8000):
        import uvicorn
        init_db()
        uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    fire.Fire(CLI)
