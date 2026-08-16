import { useEffect, useState } from 'react';
import { api } from '../lib/api';

export interface AppVersion {
  version_code: number;
  version_name: string;
  release_notes: string;
  apk_file?: string | null;
  download_url?: string | null;
  apk_url?: string | null;
  is_mandatory: boolean;
  created_at: string;
}

export function useLatestAppVersion() {
  const [version, setVersion] = useState<AppVersion | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const configuredDownloadUrl = import.meta.env.VITE_APK_DOWNLOAD_URL?.trim() || null;

  useEffect(() => {
    let isActive = true;

    api.get<AppVersion>('/system/latest-version/')
      .then(({ data }) => {
        if (isActive) setVersion(data);
      })
      .catch(() => {
        if (isActive) setVersion(null);
      })
      .finally(() => {
        if (isActive) setIsLoading(false);
      });

    return () => {
      isActive = false;
    };
  }, []);

  return {
    version,
    downloadUrl: version?.apk_url || version?.download_url || version?.apk_file || configuredDownloadUrl,
    isLoading,
  };
}
