"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert
} from "@mui/material";

const API_URL = "http://localhost:5000/api/chat" /* TODO: update (set in some config??) */

interface GeneratorInfo {
  [key: string]: {
    [param: string]: {
      type: string;
      description: string;
    };
  };
}

const SystemSelectionPage = () => {
  const [generators, setGenerators] = useState<GeneratorInfo>({});
  const [selectedGenerator, setSelectedGenerator] = useState<string>("");
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchGenerators = async () => {
      try {
        const response = await axios.get(API_URL + "/generators");
        setGenerators(response.data);
      } catch (err) {
        setError("Failed to load generators.");
      }
    };
    fetchGenerators();
  }, []);

  const handleParameterChange = (param: string, value: string) => {
    setParameters((prev) => ({ ...prev, [param]: value }));
  };

  const startChat = async () => {
    if (!selectedGenerator) {
      setError("Please select a generator.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(API_URL + "/init", {
        generator_name: selectedGenerator,
        parameters,
      });

      router.push(`/chat?conversation_id=${response.data.conversation_id}`);
    } catch (err) {
      setError("Error initializing chat. Please check your inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h5" gutterBottom>
        Select a Generator
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {/* Dropdown for selecting generator */}
        <FormControl fullWidth>
          <InputLabel>Select a Generator</InputLabel>
          <Select
            value={selectedGenerator}
            onChange={(e) => {
              setSelectedGenerator(e.target.value);
              setParameters({});
            }}
          >
            {Object.keys(generators).map((generator) => (
              <MenuItem key={generator} value={generator}>
                {generator}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Dynamic input fields for parameters */}
        {selectedGenerator &&
          Object.entries(generators[selectedGenerator]).map(([param, details]) => (
            <TextField
              key={param}
              label={details.description}
              placeholder={`Enter ${param}`}
              fullWidth
              onChange={(e) => handleParameterChange(param, e.target.value)}
            />
          ))}

        {/* Start Chat Button */}
        <Button
          variant="contained"
          color="primary"
          onClick={startChat}
          disabled={loading}
          endIcon={loading && <CircularProgress size={20} />}
        >
          Start Chat
        </Button>
      </Box>
    </Container>
  );
};

export default SystemSelectionPage;
