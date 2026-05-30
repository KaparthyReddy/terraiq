import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store";
import { fetchFields, fetchField } from "@/store/fieldSlice";

export function useFields() {
  const dispatch = useAppDispatch();
  const { fields, loading, error } = useAppSelector((s) => s.field);

  useEffect(() => {
    dispatch(fetchFields());
  }, [dispatch]);

  return { fields, loading, error };
}

export function useField(id: string) {
  const dispatch = useAppDispatch();
  const selected = useAppSelector((s) => s.field.selected);

  useEffect(() => {
    if (id) dispatch(fetchField(id));
  }, [dispatch, id]);

  return selected;
}
