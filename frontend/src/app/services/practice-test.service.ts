import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GenerateTestResponse } from '../models/test-models';

@Injectable({
  providedIn: 'root'
})
export class PracticeTestService {
  private baseURL = '/api/academics/practice_test';

  constructor(private http: HttpClient) {}

  deleteTest(testId: number): Observable<any> {
    return this.http.delete(`${this.baseURL}/delete_response/${testId}`);
  }
  getTest(testID: number): Observable<any> {
    return this.http.get(`${this.baseURL}/retrieve_response/${testID}`);
  }

  generateTest(data: { prompt: string; formats: string[], resource_ids: number[] }) {
    return this.http.post<GenerateTestResponse>(
      `${this.baseURL}/generate_test`,
      {
        prompt: data.prompt,
        formats: data.formats,
        resource_ids: data.resource_ids
      }
    );
  }
}
