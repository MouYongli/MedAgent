// app/(auth)/sign-in/page.tsx
'use client';

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Container
} from '@mui/material';

interface FormValues {
  username: string;
  password: string;
}

const SignInPage: React.FC = () => {
  const [values, setValues] = React.useState<FormValues>({
    username: '',
    password: ''
  });
  const [errors, setErrors] = React.useState<Partial<FormValues>>({});

  const handleChange = (prop: keyof FormValues) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({ ...values, [prop]: event.target.value });
    // Clear error when user starts typing
    if (errors[prop]) {
      setErrors({ ...errors, [prop]: undefined });
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    
    // Validation
    const newErrors: Partial<FormValues> = {};
    if (!values.username) {
      newErrors.username = 'Please enter the username!';
    }
    if (!values.password) {
      newErrors.password = 'Please enter the password!';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    //TODO
    console.log('Login Information', values);
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5" gutterBottom>
            Sign In
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={values.username}
              onChange={handleChange('username')}
              error={!!errors.username}
              helperText={errors.username}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={values.password}
              onChange={handleChange('password')}
              error={!!errors.password}
              helperText={errors.password}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default SignInPage;
