import sys
import time
import fire
from bharatwatch.core.database import init_db
from bharatwatch.core.orchestrator import run_all, run_module
from bharatwatch.core.healer import heal_monitor, heal_source, heal_source_with_retries
from bharatwatch.api.main import app

class CLI:
    def init_db(self):
        init_db()
        print("Database initialized.")

    def run_all(self, auto_heal: bool = True):
        """Run every collector once; auto-heal any source that breaks."""
        init_db()
        run_all()

    def run_module(self, module: str):
        init_db()
        run_module(module)

    def heal(self, source_id: int, description: str = "", retries: bool = True):
        """Manually heal one source, closed-loop (auto-approve + validate)."""
        init_db()
        if retries:
            result = heal_source_with_retries(source_id)
        else:
            result = heal_source(source_id, description=description or None)
        print(result)

    def heal_monitor(self):
        """One pass: heal every broken/unknown source, closed-loop."""
        init_db()
        heal_monitor()

    def watch(self, interval: int = 300):
        """Real-time monitor: run all collectors, auto-heal failures, repeat.

        interval = seconds between full sweeps (default 300 = 5 min).
        Ctrl-C to stop. This is the always-on self-healing daemon.
        """
        init_db()
        print(f"[watch] self-healing monitor started (interval={interval}s). Ctrl-C to stop.")
        try:
            while True:
                print(f"[watch] sweep @ {time.strftime('%H:%M:%S')}")
                run_all()                       # auto-heal is built into run_source
                recovered = heal_monitor()      # catch anything still broken
                if recovered:
                    ok = sum(1 for r in recovered if r.get("success"))
                    print(f"[watch] healed {ok}/{len(recovered)} broken sources")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[watch] stopped.")

    def serve(self, host="127.0.0.1", port=8000):
        import uvicorn
        init_db()
        uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    fire.Fire(CLI)
