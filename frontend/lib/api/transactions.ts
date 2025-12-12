import apiClient from './client';

export interface Transaction {
  id: number;
  amount: string;
  type: 'income' | 'expense';
  date: string;
  description: string;
  category: number;
  category_name?: string;
  category_color?: string;
  tags: number[];
  tags_list?: string[];
  created_at: string;
  updated_at: string;
}

export interface TransactionFilters {
  type?: 'income' | 'expense';
  category?: number;
  start_date?: string;
  end_date?: string;
  search?: string;
}

export interface TransactionSummary {
  start_date: string;
  end_date: string;
  total_income: number;
  total_expenses: number;
  balance: number;
  transaction_count: number;
}

export const transactionsAPI = {
  getAll: async (filters?: TransactionFilters) => {
    const response = await apiClient.get('/transactions/', { params: filters });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get(`/transactions/${id}/`);
    return response.data;
  },

  create: async (data: Partial<Transaction>) => {
    const response = await apiClient.post('/transactions/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Transaction>) => {
    const response = await apiClient.patch(`/transactions/${id}/`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/transactions/${id}/`);
  },

  getSummary: async (startDate?: string, endDate?: string): Promise<TransactionSummary> => {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await apiClient.get('/transactions/summary/', { params });
    return response.data;
  },
};

