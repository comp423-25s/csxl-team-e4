export interface GenerateTestResponse {
    response_id: string;
  }
  
  export interface PracticeTest {
    id: string;
    prompt: string;
    formats: string[];
    material: number;
    createdAt?: string;
  }
  