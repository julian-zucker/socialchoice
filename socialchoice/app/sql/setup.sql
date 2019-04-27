CREATE TABLE candidates
(
  id   SERIAL PRIMARY KEY,
  name VARCHAR(300)
);

CREATE TABLE votes
(
  id              SERIAL PRIMARY KEY,
  submission_time TIMESTAMP NOT NULL DEFAULT NOW(),
  candidate1      INTEGER REFERENCES candidates(id),
  candidate2      INTEGER REFERENCES candidates(id),
  result          vote_result
);

CREATE TYPE vote_result AS ENUM ('win', 'loss', 'tie');
