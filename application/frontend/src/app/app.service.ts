import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AppService {
  messageArray: any[] = [];

  constructor(private httpClient: HttpClient) {}

  get_response(data: any) {
    let url = 'http://localhost:8080/chat';
    return this.httpClient.post(url, data);
  }

  clear_history() {
    let url = 'http://localhost:8080/clear';
    return this.httpClient.get(url);
  }
}
