import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { Container, Typography, Box, Button, Grid, Paper } from '@mui/material';
import { authAPI } from '@/lib/api/auth';

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        await authAPI.getProfile();
        setIsAuthenticated(true);
      }
    } catch (error) {
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
          <Typography>Loading...</Typography>
        </Box>
      </Container>
    );
  }

  if (!isAuthenticated) {
    return (
      <Container>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
          <Typography variant="h3" component="h1" gutterBottom>
            Personal Finance Manager
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Manage your income, expenses, budgets, and savings goals
          </Typography>
          <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
            <Button variant="contained" onClick={() => router.push('/login')}>
              Login
            </Button>
            <Button variant="outlined" onClick={() => router.push('/register')}>
              Register
            </Button>
          </Box>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Transactions
            </Typography>
            <Typography variant="body2" color="text.secondary">
              View and manage your income and expenses
            </Typography>
            <Button variant="contained" sx={{ mt: 2 }} onClick={() => router.push('/transactions')}>
              View Transactions
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Budgets
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Set and track your monthly budgets
            </Typography>
            <Button variant="contained" sx={{ mt: 2 }} onClick={() => router.push('/budgets')}>
              View Budgets
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Savings Goals
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Track your savings progress
            </Typography>
            <Button variant="contained" sx={{ mt: 2 }} onClick={() => router.push('/savings-goals')}>
              View Goals
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
