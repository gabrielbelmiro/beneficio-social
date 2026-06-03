import { Routes } from '@angular/router';
import { ManualReviewListComponent } from './features/manual-reviews/manual-review-list/manual-review-list';
import { AuditLogListComponent } from './features/audit-logs/audit-log-list/audit-log-list';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  {
    path: 'manual-reviews',
    component: ManualReviewListComponent,
    canActivate: [authGuard],
  },
  {
    path: 'audit-logs',
    component: AuditLogListComponent,
    canActivate: [authGuard],
  },
];
