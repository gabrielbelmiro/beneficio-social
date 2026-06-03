import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// Use project root path for environments (resolves module lookup issues)
import { environment } from 'environments/environment';

export interface AuditLog {
  id: number;
  user_email?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  status: string;
  details?: string;
  execution_id?: string;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class AuditLogService {
  constructor(private http: HttpClient) {}

  listAuditLogs() {
    return this.http.get<AuditLog[]>(`${environment.apiUrl}/audit-logs`);
  }
}