import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store";
import { fetchLatest, fetchHistory } from "@/store/sensorSlice";

export function useLatestReading(fieldId: string) {
  const dispatch = useAppDispatch();
  const { latest, loading } = useAppSelector((s) => s.sensor);

  useEffect(() => {
    if (!fieldId) return;
    dispatch(fetchLatest(fieldId));
    const interval = setInterval(() => dispatch(fetchLatest(fieldId)), 30_000);
    return () => clearInterval(interval);
  }, [dispatch, fieldId]);

  return { latest, loading };
}

export function useSensorHistory(fieldId: string) {
  const dispatch = useAppDispatch();
  const history = useAppSelector((s) => s.sensor.history);

  useEffect(() => {
    if (fieldId) dispatch(fetchHistory(fieldId));
  }, [dispatch, fieldId]);

  return history;
}
