import apiClient from './client';

export interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  color: string;
  icon: string;
  transaction_count?: number;
  created_at: string;
  updated_at: string;
}

export const categoriesAPI = {
  getAll: async (type?: 'income' | 'expense') => {
    const params = type ? { type } : {};
    const response = await apiClient.get('/categories/', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get(`/categories/${id}/`);
    return response.data;
  },

  create: async (data: Partial<Category>) => {
    const response = await apiClient.post('/categories/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Category>) => {
    const response = await apiClient.patch(`/categories/${id}/`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/categories/${id}/`);
  },
};

