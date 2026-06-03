import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  ManualReview,
  ManualReviewService
} from '../../../core/services/manual-review.service';

@Component({
  selector: 'app-manual-review-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manual-review-list.component.html'
})
export class ManualReviewListComponent implements OnInit {
  reviews: ManualReview[] = [];
  reasons: Record<number, string> = {};
  loading = false;

  constructor(private manualReviewService: ManualReviewService) {}

  ngOnInit(): void {
    this.loadReviews();
  }

  loadReviews(): void {
    this.loading = true;

    this.manualReviewService.listPending().subscribe({
      next: (reviews) => {
        this.reviews = reviews;
        this.loading = false;
      },
      error: () => {
        alert('Erro ao carregar revisões pendentes.');
        this.loading = false;
      }
    });
  }

  decide(review: ManualReview, decision: 'APPROVED' | 'REJECTED'): void {
    const reason = this.reasons[review.id];

    if (!reason || reason.trim().length < 5) {
      alert('Informe um motivo com pelo menos 5 caracteres.');
      return;
    }

    this.manualReviewService.decide(review.id, decision, reason).subscribe({
      next: () => {
        alert(`Revisão finalizada como ${decision}.`);
        this.loadReviews();
      },
      error: () => {
        alert('Erro ao finalizar revisão.');
      }
    });
  }
}