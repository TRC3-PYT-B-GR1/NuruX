import React from 'react';
import { cn } from '../../lib/utils';

interface Column {
  header: string;
  accessor: string;
  cell?: (item: any) => React.ReactNode;
}

interface TableProps {
  columns: Column[];
  data: any[];
  className?: string;
}

export function Table({ columns, data, className }: TableProps) {
  return (
    <div className={cn("w-full overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm", className)}>
      <table className="w-full text-left text-sm text-slate-600">
        <thead className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500">
          <tr>
            {columns.map((col, idx) => (
              <th key={idx} className="px-6 py-4 font-semibold tracking-wider">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-8 text-center text-slate-500">
                No data available.
              </td>
            </tr>
          ) : (
            data.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-slate-50 transition-colors">
                {columns.map((col, colIndex) => (
                  <td key={colIndex} className="px-6 py-4 whitespace-nowrap">
                    {col.cell ? col.cell(row) : row[col.accessor]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
