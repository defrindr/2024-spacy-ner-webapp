import subprocess
class CrawlerHelper():
    def run(self, path, keyword, limit=10, token=''):
        command = f'npx -y tweet-harvest@2.6.1 -o "{path}" -s "{keyword}" --tab "LATEST" -l {limit} --token "{token}"'
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print("Command output:", result.stdout)  # Print stdout
            print("Command error output:", result.stderr)  # Print stderr
            if result.returncode != 0:
                return True
        except subprocess.CalledProcessError as e:
            # Print error to console for debugging
            print(f'Error occurred: {e}\n{e.stderr}')
            # Include stderr in the flash message
            return False
