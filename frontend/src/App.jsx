import { useState } from "react";
import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  Container,
  IconButton,
  InputBase,
  Paper,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { RemoteRunnable } from "langchain/runnables/remote";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const search = async () => {
    const chain = new RemoteRunnable({
      url: `http://localhost:8000/legal/`,
    });
    const result = await chain.invoke(query);

    setResponse(result);
  };

  return (
    <Container maxWidth="l">
      <Box sx={{ my: 4 }} style={{ textAlign: "center" }}>
        <Typography variant="h2" component="h1" sx={{ mb: 2 }}>
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

      {response && (
        <Box
          sx={{ my: 4 }}
          style={{ display: "flex", justifyContent: "center" }}
        >
          <Card sx={{ maxWidth: 345 }}>
            <CardActionArea>
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  Answer by AI
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {response}
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Box>
      )}
    </Container>
  );
}

export default App;
