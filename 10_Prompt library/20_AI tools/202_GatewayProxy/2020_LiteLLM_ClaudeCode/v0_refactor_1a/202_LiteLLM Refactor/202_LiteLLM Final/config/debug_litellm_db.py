import asyncio
import os
import sys

# Add current directory to path just in case
sys.path.append(os.getcwd())

# Mock ProxyLogging
class MockProxyLogging:
    def debug(self, msg, *args): print(f"DEBUG: {msg} {args}")
    def info(self, msg, *args): print(f"INFO: {msg} {args}")
    def warning(self, msg, *args): print(f"WARNING: {msg} {args}")
    def error(self, msg, *args): print(f"ERROR: {msg} {args}")
    def failure_handler(self, *args, **kwargs): 
        print(f"FAILURE HANDLER: {args} {kwargs}")
        async def _noop(): pass
        return _noop()

async def main():
    print("--- Starting Debug ---")
    
    # Set env var
    db_url = "file:C:/Users/YC/LiteLLM/litellm.db"
    os.environ["DATABASE_URL"] = db_url
    print(f"DATABASE_URL: {os.environ['DATABASE_URL']}")

    print("\n--- Testing LiteLLM Wrapper ---")
    try:
        from litellm.proxy.utils import PrismaClient
        
        proxy_logging = MockProxyLogging()
        
        print("Instantiating LiteLLM PrismaClient...")
        litellm_client = PrismaClient(
            database_url=db_url,
            proxy_logging_obj=proxy_logging
        )
        print("LiteLLM PrismaClient instantiated.")
        
        print("Connecting...")
        await litellm_client.connect()
        print("Connected!")

        print("Running health check...")
        try:
            res = await litellm_client.health_check()
            print(f"Health check result: {res}")
        except Exception as e:
            print(f"Health check failed: {e}")

        print("Disconnecting...")
        await litellm_client.disconnect()
        print("Disconnected!")

    except Exception as e:
        print(f"LiteLLM Wrapper Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
