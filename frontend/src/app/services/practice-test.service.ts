import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';




@Injectable({
  providedIn: 'root'
})
export class PracticeTestService {
  private baseURL = '/api/academics/practice_test';

  constructor(private http: HttpClient) { }

  deleteTest(testId: number): Observable<any> {
    return this.http.delete(`${this.baseURL}/delete_response/${testId}`);
  }
  getTest(testID: number): Observable<any> {
    return this.http.get(`${this.baseURL}/retrieve_response/${testID}`);
  }
  generateTest(inputText: string): Observable<any> {
    return this.http.post(`${this.baseURL}/generate_test`, {
      text: inputText,
      image: null,
      file: null
    });
  }
}

