import re

with open("omlx/optimization/manager.py", "r") as f:
    content = f.read()

content = content.replace("def get_execution_order(self) -> List[BasePass]:", "def get_execution_order(self, stage=None) -> List[BasePass]:")

new_code = """        passes = self.get_registered_passes()

        if stage is not None:
            passes = [p for p in passes if stage in p.supported_stages]

        # Validation"""

content = content.replace("        passes = self.get_registered_passes()\n\n        # Validation", new_code)

with open("omlx/optimization/manager.py", "w") as f:
    f.write(content)
