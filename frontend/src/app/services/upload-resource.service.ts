import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
// Think of it as analagous to practice-test-service, without needing form builder injection like practice-test-form-service.
// logic for form that contains file title and pdf for upload. The backend will conv. No need to inj. form builder, fairly lightweight form.
export class UploadResourceService {
  private baseURL = '/api/academics/resources';

  constructor(private http: HttpClient) {}

  uploadResource(title: string, file: File, fileName: string, courseId: string): Observable<any> {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);
    formData.append('file_name', fileName);
    formData.append('course_id', courseId);
    
    return this.http.post(`${this.baseURL}/upload`, formData);
  }
}
