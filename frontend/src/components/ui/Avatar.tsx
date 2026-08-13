import { cn } from '../../lib/utils';

interface AvatarProps {
  src?: string;
  alt: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizes = {
  sm: 'h-8 w-8',
  md: 'h-10 w-10',
  lg: 'h-12 w-12',
};

export function Avatar({ src, alt, size = 'md', className }: AvatarProps) {
  const initials = alt.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  
  return (
    <div className={cn(
      "rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center overflow-hidden flex-shrink-0",
      sizes[size],
      className
    )}>
      {src ? (
        <img src={src} alt={alt} className="h-full w-full object-cover" />
      ) : (
        <span className="text-slate-500 font-medium text-sm">{initials}</span>
      )}
    </div>
  );
}
