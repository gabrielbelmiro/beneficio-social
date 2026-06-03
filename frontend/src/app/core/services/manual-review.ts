import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

export interface ManualReview {
  id: number;
  document_id: number;
  client_id: number;
  status: string;
  ai_reason?: string;
  manual_reason?: string;
  final_decision?: string;
}

@Injectable({ providedIn: 'root' })
export class ManualReviewService {
  constructor(private http: HttpClient) {}

  listPending() {
    return this.http.get<ManualReview[]>(`${environment.apiUrl}/manual-reviews`);
  }

  decide(reviewId: number, finalDecision: 'APPROVED' | 'REJECTED', manualReason: string) {
    return this.http.post<ManualReview>(
      `${environment.apiUrl}/manual-reviews/${reviewId}/decision`,
      {
        final_decision: finalDecision,
        manual_reason: manualReason
      }
    );
  }
}