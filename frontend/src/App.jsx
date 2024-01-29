import { useState } from "react";
import {
  Alert,
  Box,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  IconButton,
  InputBase,
  Paper,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { RemoteRunnable } from "langchain/runnables/remote";

function App() {
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [failureResponse, setFailureResponse] = useState(false);

  const search = async () => {
    setLoading(true);
    setFailureResponse(false);
    const chain = new RemoteRunnable({
      url: `http://localhost:8000/legal/`,
    });
    const result = await chain.invoke(query);

    try {
      const json = JSON.parse(result);
      if (json.answer === "I don't know the answer.") setFailureResponse(true);
      setResponse(json);
    } catch (e) {
      setFailureResponse(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="l">
      <Box sx={{ my: 4 }} style={{ textAlign: "center" }}>
        <Typography variant="h2" component="h1">
          LLM for Legal Advisory
        </Typography>
        <Typography variant="h3" component="h3" sx={{ mb: 2 }}>
          Final Project Report in Natural Language Processing
        </Typography>
      </Box>

      <Box sx={{ my: 4 }} style={{ display: "flex", justifyContent: "center" }}>
        <Paper
          component="form"
          sx={{
            p: "2px 4px",
            display: "flex",
            alignItems: "center",
            width: 400,
          }}
        >
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="Enter your query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <IconButton
            type="button"
            sx={{ p: "10px" }}
            aria-label="search"
            onClick={search}
          >
            <SearchIcon />
          </IconButton>
        </Paper>
      </Box>

      {loading && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <CircularProgress />
        </div>
      )}

      {response && !loading && !failureResponse && (
        <Box
          sx={{ my: 8 }}
          style={{ display: "flex", justifyContent: "center" }}
        >
          <Card sx={{ maxWidth: 1045 }}>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Answer by AI
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {response.answer}
              </Typography>
            </CardContent>
            <CardActions>
              {response.articles.map((article) => (
                <Chip label={article} />
              ))}
            </CardActions>
          </Card>
        </Box>
      )}
      {failureResponse && (
        <Box
          sx={{ my: 8 }}
          style={{ display: "flex", justifyContent: "center" }}
        >
          <Alert severity="error">
            The LegalLLM can not provide an answer for this question.
          </Alert>
        </Box>
      )}
    </Container>
  );
}

export default App;
