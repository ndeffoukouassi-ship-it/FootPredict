import axios from "axios";
import { Fixture, Prediction, MatchAnalysis } from "./types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
});

export const getTodayMatches = async (): Promise<Fixture[]> => {
  const { data } = await api.get("/matches/today");
  return data;
};

export const getFixture = async (id: number): Promise<Fixture> => {
  const { data } = await api.get(`/matches/${id}`);
  return data;
};

export const getMatchAnalysis = async (id: number): Promise<MatchAnalysis> => {
  const { data } = await api.get(`/matches/${id}/analysis`);
  return data;
};

export const getPrediction = async (id: number): Promise<Prediction> => {
  const { data } = await api.get(`/predictions/${id}`);
  return data;
};
