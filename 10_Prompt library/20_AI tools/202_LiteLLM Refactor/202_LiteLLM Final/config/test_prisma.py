import asyncio
from prisma import Prisma
import os

# Ensure DATABASE_URL is set
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "file:C:/Users/YC/LiteLLM/litellm.db"

async def main():
    print(f"Connecting to {os.environ['DATABASE_URL']}...")
    try:
        db = Prisma()
        await db.connect()
        print("Connected successfully!")
        await db.disconnect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
