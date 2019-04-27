from cloudfunction import cloudfunction


@cloudfunction(in_schema={
    "type": "object",
    "properties": {
        "candidate1": {"type": "string"},
        "candidate2": {"type": "string"},
        "result": {"enum": ["win", "loss", "tie"]}
    }},
    out_schema={})
def submit_vote(request_json, conn):
    c1 = request_json["candidate1"]
    c2 = request_json["candidate2"]
    result = request_json["result"]

    conn.execute("""
    INSERT INTO votes(candidate1, candidate2, result) VALUES (%s, %s, %s) 
    """, (c1, c2, result))
