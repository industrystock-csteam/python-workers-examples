import json
from urllib.parse import urlparse, parse_qs

from workers import Response, WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)

        if url.path == "/":
            return Response(
                "Python Worker läuft!",
                headers={"Content-Type": "text/plain"}
            )

        if url.path == "/calculate":
            params = parse_qs(url.query)
            try:
                zahl = float(params.get("zahl", ["0"])[0])
            except ValueError:
                return Response(
                    json.dumps({"error": "Ungueltige Zahl"}),
                    status=400,
                    headers={"Content-Type": "application/json"}
                )

            ergebnis = zahl ** 2

            return Response(
                json.dumps({
                    "zahl": zahl,
                    "ergebnis": ergebnis
                }),
                headers={"Content-Type": "application/json"}
            )

        return Response("Not Found", status=404)
