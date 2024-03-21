import os
import nox
import shutil


@nox.session
def docs(session: nox.Session) -> None:
    # session.install("-r", "docs/requirements-docs.txt")
    # session.install(".[socks,brotli,zstd]")

    session.run("sphinx-apidoc", "-o", "docs", "ranch")

    session.chdir("docs")
    if os.path.exists("_build"):
        try:
            shutil.rmtree("_build")
        except:
            print("_build folder cannot removed")
    session.run("make", "html")
    # session.run("sphinx-build", "-b", "html", "-W", "src", "_build/html")
