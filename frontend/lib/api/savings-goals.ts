import apiClient from './client';

export interface SavingsGoal {
  id: number;
  name: string;
  target_amount: string;
  current_amount: string;
  deadline?: string;
  progress_percentage?: number;
  remaining_amount?: string;
  created_at: string;
  updated_at: string;
}

export const savingsGoalsAPI = {
  getAll: async () => {
    const response = await apiClient.get('/savings-goals/');
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get(`/savings-goals/${id}/`);
    return response.data;
  },

  create: async (data: Partial<SavingsGoal>) => {
    const response = await apiClient.post('/savings-goals/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<SavingsGoal>) => {
    const response = await apiClient.patch(`/savings-goals/${id}/`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/savings-goals/${id}/`);
  },

  addAmount: async (id: number, amount: number) => {
    const response = await apiClient.post(`/savings-goals/${id}/add_amount/`, { amount });
    return response.data;
  },
};

