import re

input_path = r"C:\Users\YC\LiteLLM\schema.prisma"
output_path = r"C:\Users\YC\LiteLLM\schema.sqlite.prisma"

with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace provider
content = content.replace('provider = "postgresql"', 'provider = "sqlite"')

# 2. Replace Json with String
content = re.sub(r'\bJson\b', 'String', content)

# 3. Remove enum JobStatus block
content = re.sub(r'enum\s+JobStatus\s*\{[^}]*\}', '', content, flags=re.DOTALL)

# 4. Replace usages of JobStatus with String
content = re.sub(r'\bJobStatus\b', 'String', content)

# 5. Fix INACTIVE default
content = content.replace('@default(INACTIVE)', '@default("INACTIVE")')

# 6. Replace Scalar[] with String
# Only replace known scalar types
scalar_types = ['String', 'Boolean', 'Int', 'BigInt', 'Float', 'Decimal', 'DateTime', 'Bytes']
for t in scalar_types:
    # Pattern: Type[] -> String
    content = re.sub(rf'\b{t}\[\]', 'String', content)

# 7. Fix empty list defaults @default([]) -> @default("[]")
content = content.replace('@default([])', '@default("[]")')

with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Created {output_path}")
