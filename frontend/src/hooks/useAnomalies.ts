import { useTeamAttendance } from './useTeamAttendance';

export function useAnomalies() {
  const { data, isLoading, error } = useTeamAttendance();
  
  // Filter for records that are flagged as anomalies
  const anomalies = data?.raw.filter(record => record.is_anomaly) || [];
  
  return {
    anomalies,
    isLoading,
    error
  };
}
