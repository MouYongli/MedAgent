'use client';

import React from 'react';
import { TextField, Button, Box } from '@mui/material';

const SignInPage: React.FC = () => {
  const onFinish = (values: any) => {
    //TODO
    console.log('Login Information', values);
  };

  return (
    <Box sx={{ maxWidth: 300, margin: '50px auto', padding: '20px', boxShadow: '0 0 10px rgba(0,0,0,0.1)' }}>
      <h2 style={{ textAlign: 'center' }}>Sign In</h2>
      <form onSubmit={onFinish}>
        <TextField
          label="Username"
          name="username"
          required
          fullWidth
          margin="normal"
          placeholder="Please enter the username"
        />
        <TextField
          label="Password"
          name="password"
          type="password"
          required
          fullWidth
          margin="normal"
          placeholder="Please enter the password"
        />
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Sign In
        </Button>
      </form>
    </Box>
  );
};

export default SignInPage;
