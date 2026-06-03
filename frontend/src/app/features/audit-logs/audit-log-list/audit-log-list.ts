import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  AuditLog,
  AuditLogService
} from '../../../core/services/audit-log.service';

@Component({
  selector: 'app-audit-log-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audit-log-list.component.html'
})
export class AuditLogListComponent implements OnInit {
  logs: AuditLog[] = [];
  loading = false;

  constructor(private auditLogService: AuditLogService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.loading = true;

    this.auditLogService.listAuditLogs().subscribe({
      next: (logs) => {
        this.logs = logs;
        this.loading = false;
      },
      error: () => {
        alert('Erro ao carregar auditoria.');
        this.loading = false;
      }
    });
  }
}