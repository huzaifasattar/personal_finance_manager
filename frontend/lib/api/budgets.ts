import apiClient from './client';

export interface Budget {
  id: number;
  category: number;
  category_name?: string;
  amount: string;
  period: 'monthly' | 'yearly';
  year: number;
  month?: number;
  spent_amount?: number;
  remaining_amount?: number;
  progress_percentage?: number;
  created_at: string;
  updated_at: string;
}

export const budgetsAPI = {
  getAll: async (year?: number, period?: 'monthly' | 'yearly') => {
    const params: any = {};
    if (year) params.year = year;
    if (period) params.period = period;
    
    const response = await apiClient.get('/budgets/', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get(`/budgets/${id}/`);
    return response.data;
  },

  create: async (data: Partial<Budget>) => {
    const response = await apiClient.post('/budgets/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Budget>) => {
    const response = await apiClient.patch(`/budgets/${id}/`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/budgets/${id}/`);
  },
};

