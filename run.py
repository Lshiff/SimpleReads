#finalproject is __init__.py
from finalproject import app

import sys
print(sys.path)


if __name__ == "__main__":
    app.run(debug=True)
