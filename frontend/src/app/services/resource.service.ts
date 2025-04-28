import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Resource {
  id: number;
  title: string;
  file_name: string;
  ta_upload: Boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ResourceService {
  private baseUrl = '/api/academics/resources';

  constructor(private http: HttpClient) {}
  getResources(course_id?: string): Observable<Resource[]> {
    const params = course_id ? { params: { course_id } } : {};
    return this.http.get<Resource[]>(this.baseUrl + '/', params);
  }

  deleteResource(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  downloadResource(id: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${id}/download`, {
      responseType: 'blob'
    });
  }
}
