import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Resource {
  id: number;
  title: string;
  file_name: string;
}

@Injectable({
  providedIn: 'root',
})
export class ResourceService {
  private baseUrl = '/api/academics/resources';

  constructor(private http: HttpClient) {}

  getResources(): Observable<Resource[]> {
    return this.http.get<Resource[]>(this.baseUrl + '/');
  }
  

  deleteResource(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  downloadResource(id: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${id}/download`, {
      responseType: 'blob',
    });
  }
}
